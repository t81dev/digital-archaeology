#!/usr/bin/env python3
"""
Tests for Hugging Face Model Repository & Load Contract Simulator.
"""

import json
import pytest
from reconstructions.huggingface_hub_contract.hf_hub_sim import (
    ModelCardParser,
    SafeTensorsHeader,
    HuggingFaceHubServer,
    LocalCache,
    AutoConfig,
    AutoModel,
    AutoTokenizer,
    pipeline,
    LlamaForCausalLM,
    BertForSequenceClassification
)


@pytest.fixture
def mock_hub_and_cache():
    hub = HuggingFaceHubServer()
    cache = LocalCache()

    llama_card = """---
license: apache-2.0
tags:
- text-generation
pipeline_tag: text-generation
---
# Llama Model Card
"""
    llama_files = {
        "config.json": json.dumps({"model_type": "llama", "vocab_size": 1000, "hidden_size": 512}),
        "model.safetensors.header": json.dumps({"weight": {"dtype": "F32", "shape": [512, 512], "data_offsets": [0, 1024]}}),
        "tokenizer.json": json.dumps({"vocab": {"<unk>": 0, "hello": 1, "world": 2}}),
        "tokenizer_config.json": json.dumps({"chat_template": "User: {content}"}),
        "README.md": llama_card
    }
    hub.register_repository("test/llama-repo", llama_files, gated=True, commit_sha="sha_llama_123")

    bert_card = """---
license: mit
tags:
- classification
pipeline_tag: text-classification
---
# BERT Card
"""
    bert_files = {
        "config.json": json.dumps({"model_type": "bert", "num_labels": 2}),
        "model.safetensors.header": json.dumps({"classifier": {"dtype": "F32", "shape": [2, 512], "data_offsets": [0, 512]}}),
        "tokenizer.json": json.dumps({"vocab": {"<unk>": 0, "good": 1, "bad": 2}}),
        "tokenizer_config.json": json.dumps({}),
        "README.md": bert_card
    }
    hub.register_repository("test/bert-repo", bert_files, gated=False, commit_sha="sha_bert_456")

    return hub, cache


def test_model_card_parser():
    card_md = """---
license: apache-2.0
tags:
- llm
- text-generation
pipeline_tag: text-generation
---
# Test Model
Body content here.
"""
    parsed = ModelCardParser.parse(card_md)
    assert parsed["license"] == "apache-2.0"
    assert "llm" in parsed["tags"]
    assert parsed["pipeline_tag"] == "text-generation"
    assert "Body content here." in parsed["_body"]

    valid, missing = ModelCardParser.validate(parsed)
    assert valid is True
    assert len(missing) == 0


def test_safetensors_header():
    tensors = {"layer1.weight": {"dtype": "F32", "shape": [64, 64], "data_offsets": [0, 256]}}
    st = SafeTensorsHeader(tensors)
    serialized = st.serialize()
    deserialized = SafeTensorsHeader.deserialize_header(serialized)
    assert "layer1.weight" in deserialized
    assert deserialized["layer1.weight"]["shape"] == [64, 64]


def test_gated_repo_access(mock_hub_and_cache):
    hub, cache = mock_hub_and_cache
    with pytest.raises(PermissionError):
        AutoConfig.from_pretrained("test/llama-repo", hub, cache)

    config = AutoConfig.from_pretrained("test/llama-repo", hub, cache, token="valid_token")
    assert config["model_type"] == "llama"


def test_auto_model_dispatch(mock_hub_and_cache):
    hub, cache = mock_hub_and_cache
    llama_model = AutoModel.from_pretrained("test/llama-repo", hub, cache, token="token_123")
    assert isinstance(llama_model, LlamaForCausalLM)

    bert_model = AutoModel.from_pretrained("test/bert-repo", hub, cache)
    assert isinstance(bert_model, BertForSequenceClassification)


def test_tokenizer_and_chat_template(mock_hub_and_cache):
    hub, cache = mock_hub_and_cache
    tokenizer = AutoTokenizer.from_pretrained("test/llama-repo", hub, cache, token="token_123")
    encoded = tokenizer.encode("hello world")
    assert encoded == [1, 2]

    chat = tokenizer.apply_chat_template([{"role": "user", "content": "hi"}])
    assert chat == "User: hi"


def test_pipeline_execution(mock_hub_and_cache):
    hub, cache = mock_hub_and_cache
    gen_pipe = pipeline("text-generation", "test/llama-repo", hub, cache, token="token_123")
    res_gen = gen_pipe("hello world")
    assert "generated_text" in res_gen[0]

    cls_pipe = pipeline("text-classification", "test/bert-repo", hub, cache)
    res_cls = cls_pipe("good")
    assert "label" in res_cls[0]
    assert "score" in res_cls[0]
