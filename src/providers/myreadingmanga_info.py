from src.provider import Provider


class MyReadingMangaInfo(Provider):
    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self, no_increment=False) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/{}/'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('\\.info/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        content = self.get_storage_content()
        v = [self.get_url()]  # current chapter
        parser = self.document_fromstring(content, '.entry-content p > a')
        v += parser
        return v[::-1]

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        selector = '.entry-content div img,.entry-content p img'
        parser = self.html_fromstring(self.get_current_chapter(), selector)
        return [i.get('src') for i in parser]


main = MyReadingMangaInfo
