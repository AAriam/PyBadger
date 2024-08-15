"""PyBadger base badge."""

from __future__ import annotations

from markitup.html import element as _html
import pylinks as _pylinks

from pybadger.param_type import AttrDict as _AttrDict


class Badge:
    """Base Badge.

    All platform-specific badges inherit from this class.
    """
    def __init__(
        self,
        url: str | _pylinks.url.URL,
        params_light: _AttrDict = None,
        params_dark: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
        default_light: bool = True,
        merge_params: bool = True,
    ):
        self.url = _pylinks.url.create(str(url))
        self.params_light = params_light or {}
        self.params_dark = params_dark or {}
        self.attrs_img = attrs_img or {}
        self.attrs_a = attrs_a or {}
        self.attrs_picture = attrs_picture or {}
        self.attrs_source_light = attrs_source_light or {}
        self.attrs_source_dark = attrs_source_dark or {}
        self.default_light = default_light
        self.merge_params = merge_params
        return

    def img(
        self,
        params: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        light: bool | None = None,
        merge_params: bool | None = None,
    ) -> _html.Img | _html.A:

        default_light = light if light is not None else self.default_light
        merge_params = merge_params if merge_params is not None else self.merge_params
        if params is None:
            if default_light:
                params = self.params_light
                params_other = self.params_dark
            else:
                params = self.params_dark
                params_other = self.params_light
            if merge_params:
                params = params_other | params
        attrs_img = attrs_img if isinstance(attrs_img, dict) else self.attrs_img
        attrs_a = attrs_a if isinstance(attrs_a, dict) else self.attrs_a
        img = _html.img(src=self._generate_url(params), **attrs_img)
        if not attrs_a:
            return img
        return _html.a(img, attrs_a)

    def picture(
        self,
        params_light: _AttrDict = None,
        params_dark: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
        default_light: bool = True,
        merge_params: bool = True
    ) -> _html.Picture | _html.A:
        params_light = params_light or self.params_light
        params_dark = params_dark or self.params_dark
        if merge_params:
            params_light = params_dark | params_light
            params_dark = params_light | params_dark
        picture = _html.picture_color_scheme(
            self._generate_url(params_light),
            self._generate_url(params_dark),
            attrs_picture if isinstance(attrs_picture, dict) else self.attrs_picture,
            attrs_source_light if isinstance(attrs_source_light, dict) else self.attrs_source_light,
            attrs_source_dark if isinstance(attrs_source_dark, dict) else self.attrs_source_dark,
            attrs_img if isinstance(attrs_img, dict) else self.attrs_img,
            default_light if default_light is not None else self.default_light,
        )
        attrs_a = attrs_a if isinstance(attrs_a, dict) else self.attrs_a
        if not attrs_a:
            return picture
        return _html.a(picture, attrs_a)

    def unset_all(self) -> Badge:
        self.unset_params()
        self.unset_attrs()
        return self

    def unset_params(self) -> Badge:
        self.params_light = {}
        self.params_dark = {}
        return self

    def unset_attrs(self) -> Badge:
        self.attrs_img = {}
        self.attrs_a = {}
        self.attrs_picture = {}
        self.attrs_source_light = {}
        self.attrs_source_dark = {}
        return self

    def set(
        self,
        params_light: _AttrDict = None,
        params_dark: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
    ) -> Badge:
        self.set_params(params_light, params_dark)
        self.set_attrs(attrs_img, attrs_a, attrs_picture, attrs_source_light, attrs_source_dark)
        return self

    def set_params(self, light: dict | None = None, params_dark: dict | None = None) -> Badge:
        params_input = locals()
        for param_type in ("light", "dark"):
            params = params_input[param_type]
            if params is not None:
                new_params = getattr(self, f"params_{param_type}") | params
                setattr(self, f"params_{param_type}", new_params)
        return self

    def set_attrs(
        self,
        img: _AttrDict = None,
        a: _AttrDict = None,
        picture: _AttrDict = None,
        source_light: _AttrDict = None,
        source_dark: _AttrDict = None,
    ) -> Badge:
        attrs_input = locals()
        for attr_type in ("img", "a", "picture", "source_light", "source_dark"):
            attrs = attrs_input[attr_type]
            if attrs is not None:
                new_attrs = getattr(self, f"attrs_{attr_type}") | attrs
                setattr(self, f"attrs_{attr_type}", new_attrs)
        return self

    def display(self):
        from IPython.display import HTML, display
        display(HTML(str(self)))
        return

    def __str__(self):
        element = self.picture() if bool(self.params_light) and bool(self.params_dark) else self.img()
        return str(element)

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, Badge):
            raise TypeError("Only badges can be added to badges.")
        return Badge(
            url=other.url or self.url,
            params_light=self.params_light | other.params_light,
            params_dark=self.params_dark | other.params_dark,
            attrs_img=self.attrs_img | other.attrs_img,
            attrs_a=self.attrs_a | other.attrs_a,
            attrs_picture=self.attrs_picture | other.attrs_picture,
            attrs_source_light=self.attrs_source_light | other.attrs_source_light,
            attrs_source_dark=self.attrs_source_dark | other.attrs_source_dark,
            default_light=self.default_light or other.default_light,
            merge_params=self.merge_params or other.merge_params,
        )

    def _generate_url(self, params) -> str:
        url = self.url.copy()
        return str(self._generate_full_url(url, params))

    @staticmethod
    def _generate_full_url(url: _pylinks.url.URL, params: dict[str, str | bool]) -> _pylinks.url.URL:
        url.queries |= params
        return url
