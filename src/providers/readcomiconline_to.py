from src.provider import Provider


class ReadComicOnlineTo(Provider):
    def get_archive_name(self) -> str:
        chapter = self.re.search('id=(\d+)', self.get_current_chapter()).group(1)
        return 'vol_{:0>3}-{}'.format(self._chapter_index(), chapter)

    def get_chapter_index(self, no_increment=False) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/Comic/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('\\.to/Comic/([^/]+)', self.get_url())

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), 'table.listing td > a')

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        content = self.http_get(self.get_current_chapter() + '&readType=1')
        items = self.re.findall('lstImages.push\("([^"]+)"\)', content)
        return items


main = ReadComicOnlineTo
