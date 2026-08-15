"""
Unit tests for the Qt Core Abstractions Simulator (`qt_sim.py`).
"""

import pytest
from reconstructions.qt_meta_object_signals.qt_sim import (
    ConnectionType,
    QCoreApplication,
    QEvent,
    QMetaObject,
    QObject,
    Signal,
)


class CustomWidget(QObject):
    # Signals
    valueChanged = Signal("valueChanged", int)
    clicked = Signal("clicked")

    meta_object = QMetaObject("CustomWidget", QObject.meta_object)
    meta_object.add_signal("valueChanged")
    meta_object.add_signal("clicked")
    meta_object.add_property("value")


def test_qobject_parent_child_ownership():
    QCoreApplication.clear()
    root = QObject(name="Root")
    child1 = QObject(parent=root, name="Child1")
    child2 = QObject(parent=root, name="Child2")
    grandchild = QObject(parent=child1, name="Grandchild")

    assert len(root.children()) == 2
    assert child1.parent() == root
    assert grandchild.parent() == child1

    # Destroying root recursively destroys children
    root.destroy()
    assert root._destroyed is True
    assert child1._destroyed is True
    assert child2._destroyed is True
    assert grandchild._destroyed is True


def test_meta_object_introspection():
    widget = CustomWidget()
    meta = widget.meta_object

    assert meta.class_name == "CustomWidget"
    assert meta.inherits("CustomWidget") is True
    assert meta.inherits("QObject") is True
    assert meta.inherits("QWidget") is False
    assert "valueChanged" in meta.signals
    assert "value" in meta.properties


def test_direct_signals_and_slots():
    QCoreApplication.clear()
    widget = CustomWidget()
    received_values = []

    def on_value_changed(val):
        received_values.append(val)

    widget.valueChanged.connect(on_value_changed)
    widget.valueChanged.emit(42)
    widget.valueChanged.emit(100)

    assert received_values == [42, 100]

    # Disconnect
    widget.valueChanged.disconnect(on_value_changed)
    widget.valueChanged.emit(200)
    assert received_values == [42, 100]


def test_queued_signals_and_event_loop():
    QCoreApplication.clear()
    widget = CustomWidget()
    received_values = []

    def on_value_changed(val):
        received_values.append(val)

    # Connect with QUEUED type
    widget.valueChanged.connect(on_value_changed, ConnectionType.QUEUED)
    widget.valueChanged.emit(99)

    # Immediately after emit, signal should NOT have run yet
    assert received_values == []

    # Process events in central loop
    processed = QCoreApplication.process_events()
    assert processed == 1
    assert received_values == [99]


def test_event_filter():
    QCoreApplication.clear()
    target = QObject(name="Target")
    filter_obj = QObject(name="FilterObj")

    event_log = []

    class FilteringObject(QObject):
        def event_filter(self, watched: QObject, event: QEvent) -> bool:
            event_log.append((watched.object_name(), event.type))
            if event.type == "InterceptMe":
                return True  # Intercept/Block event
            return False

    filter_obj = FilteringObject()
    target.install_event_filter(filter_obj)

    e1 = QEvent("NormalEvent")
    e2 = QEvent("InterceptMe")

    target.event(e1)
    target.event(e2)

    assert event_log == [("Target", "NormalEvent"), ("Target", "InterceptMe")]
    assert e2.accepted is True


def test_qml_declarative_property_bindings():
    QCoreApplication.clear()
    obj1 = QObject(name="Obj1")
    obj2 = QObject(name="Obj2")

    obj1.set_property("width", 100)

    # obj2.totalWidth = obj1.width * 2
    obj2.set_binding("totalWidth", lambda: obj1.property("width") * 2)

    assert obj2.property("totalWidth") == 200

    # Updating obj1 width updates obj2 totalWidth reactively
    obj1.set_property("width", 150)
    assert obj2.property("totalWidth") == 300
