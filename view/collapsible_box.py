from PySide6 import QtCore
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation
from PySide6.QtWidgets import QToolButton, QScrollArea, QSizePolicy, QFrame, QVBoxLayout, QLayout, QHBoxLayout, \
    QGroupBox, QWidget

from utils.view_util import set_children_visible


class CollapsibleBox(QGroupBox):

    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(title, parent)

        self._collapsed: bool = False
        self._initiated: bool = False
        self._is_loaded: bool = False
        self.child_layout: QLayout | None = None
        self._hidden_children: list[QWidget] = []  # 缓存已经隐藏的子控件

        self.toggle_button = QToolButton(checkable=True, checked=not self._collapsed)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        self.toggle_button.toggled.connect(self._on_toggle_released)

        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        toggle_layout.addWidget(self.toggle_button)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.contentArea = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.contentArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.contentArea.setFrameShape(QFrame.Shape.NoFrame)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(toggle_layout)
        self.layout.addWidget(self.contentArea)

        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))

    def _on_toggle_released(self):
        self._update_status()

    def setLayout(self, arg__1):
        self.layout.insertLayout(0, arg__1)

        self.child_layout = arg__1
        self._initiated = True
        self._update_status()

    def _update_status(self, force_checked: bool = False):
        checked = force_checked or self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.ArrowType.UpArrow if checked else QtCore.Qt.ArrowType.DownArrow)
        self.toggle_animation.setDirection(
            QAbstractAnimation.Direction.Forward if checked else QAbstractAnimation.Direction.Backward)
        self.toggle_animation.start()

        self._update_children()

    def _update_children(self):
        if self._collapsed != self.toggle_button.isChecked():
            return

        self._collapsed = not self._collapsed

        if self.toggle_button.isChecked():
            set_children_visible(self.child_layout, True, lambda child: self._set_child_visible(child, True))
        else:
            set_children_visible(self.child_layout, False, lambda child: self._set_child_visible(child, False))

    def _set_child_visible(self, child: QWidget, visible: bool) -> bool:
        if visible:
            for hidden_child in self._hidden_children:
                if hidden_child == child:
                    return False

            return visible
        else:
            if self._is_loaded and not child.isVisible() and child not in self._hidden_children:
                self._hidden_children.append(child)

            return visible

    def showEvent(self, event):
        self._is_loaded = True

    @property
    def collapsed(self) -> bool:
        return self._collapsed

    @collapsed.setter
    def collapsed(self, value: bool):
        self.toggle_button.setChecked(not value)
