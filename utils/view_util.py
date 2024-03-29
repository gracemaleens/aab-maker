from typing import Callable

from PySide6.QtWidgets import QLayout, QWidgetItem, QWidget


def set_children_visible(parent: QLayout, visible: bool, on_change: Callable[[QWidget], bool] = None):
    for i in range(parent.count()):
        child = parent.itemAt(i)
        if isinstance(child, QWidgetItem):
            child_widget = child.widget()
            child_widget.setVisible(on_change(child_widget) if on_change else visible)
        elif isinstance(child, QLayout):
            set_children_visible(child, visible, on_change)

