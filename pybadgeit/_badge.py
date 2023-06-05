"""Abstract base class definition for all badge objects."""


# Standard libraries
from typing import Literal, Optional
from abc import ABC, abstractmethod
# Non-standard libraries
from pylinks.url import URL
from pyhtmlit import element as html


class Badge(ABC):
    """Abstract base class for badges."""

    @abstractmethod
    def url(self, mode: Literal['dark', 'light', 'clean'] = 'clean') -> str | URL:
        """
        URL of the badge image.

        Parameters
        ----------
        mode : {'dark', 'light', 'clean'}
            'dark' and 'light' provide the URL of the badge image customized for dark and light themes,
            respectively, while 'clean' gives the URL of the badge image without any customization.

        Returns
        -------
        Any object whose __str__ method returns the desired URL. This could be a string, or any other object,
        such as a `pylinks.url.URL` object.
        """
        ...

    def __init__(
            self,
            alt: Optional[str],
            title: Optional[str],
            width: Optional[str],
            height: Optional[str],
            align: Optional[str],
            link: Optional[str | URL],
            default_theme: Literal['light', 'dark'],
    ):
        """
        Parameters
        ----------
        alt : str
            Alternative text to show if image doesn't load.
            Corresponds to the 'alt' attribute of the IMG element in HTML.
        title : str
            Description to show on mouse hover.
            Corresponds to the 'title' attribute of the IMG element in HTML.
        width : str
            Width of the image, e.g. '100px', '80%'.
            Corresponds to the 'width' attribute of the IMG element in HTML.
        height : str
            Height of the image, e.g. '100px', '80%'.
            Corresponds to the 'height' attribute of the IMG element in HTML.
        link : pylinks.URL
            Link URL, i.e. the URL that opens when clicking on the badge.
            Corresponds to the 'href' attribute of the A (anchor) element in HTML.
        default_theme : {'light', 'dark'}
            The default theme to choose e.g. when the browser doesn't support light/dark themes.
        """
        self.alt = alt
        self.title = title
        self.width = width
        self.height = height
        self.align = align
        self.link = link
        self.default_theme = default_theme
        return

    def as_html_picture(
            self, link: bool = True, html_tag_sep: str = '\n', html_line_indent: str = '\t'
    ) -> html.PICTURE | html.A:
        """
        The badge as an HTML 'picture' element, that may be wrapped by an anchor ('a') element.

        Parameters
        ----------
        link : bool, default: True
            Whether to wrap the picture element in an anchor element, to link to the address defined in `self.link`.

        Returns
        -------
        html_element : pyhtmlit.element.PICTURE | pyhtmlit.element.A
            An HTML element from the `pyhtmlit` package, which among others, has a __str__ method to
            output the HTML syntax of the element.
        """
        picture = html.PICTURE(
            img=self.as_html_img(link=False, html_tag_sep=html_tag_sep, html_line_indent=html_line_indent),
            sources=[
                html.SOURCE(srcset=self.url('dark'), media="(prefers-color-scheme: dark)"),
                html.SOURCE(srcset=self.url('light'), media="(prefers-color-scheme: light)")
            ],
            tag_seperator=html_tag_sep,
            content_indent=html_line_indent
        )
        return html.A(href=self.link, content=[picture]) if (link and self.link is not None) else picture

    def as_html_img(self, link: bool = True, html_tag_sep: str = '\n', html_line_indent: str = '\t'):
        """
        The badge as an HTML 'img' element, that may be wrapped by an anchor ('a') element.

        Parameters
        ----------
        link : bool, default: True
            Whether to wrap the img element in an anchor element, to link to the address defined in `self.link`.

        Returns
        -------
        html_element : pyhtmlit.element.IMG | pyhtmlit.element.A
            An HTML element from the `pyhtmlit` package, which among others, has a __str__ method to
            output the HTML syntax of the element.
        """
        img = html.IMG(
            src=self.url(self.default_theme),
            alt=self.alt,
            title=self.title,
            width=self.width,
            height=self.height,
            align=self.align,
        )
        if link and self.link:
            return html.A(href=self.link, content=[img], content_sep=html_tag_sep, indent=html_line_indent)
        return img

    def __str__(self):
        return str(self.as_html_picture())

    @property
    def link(self) -> URL | None:
        """URL of the badge's anchor, i.e. where it links to."""
        return self._link

    @link.setter
    def link(self, value):
        self._link = None if not value else URL(str(value))

    def display(self):
        from IPython.display import display, HTML
        display(HTML(str(self)))
        return
