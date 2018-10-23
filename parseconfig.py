import configparser
import os


class ParseConfig(configparser.ConfigParser, configparser.NoSectionError):
    def __init__(self):
        super(ParseConfig, self).__init__()

    def optionxform(self, optionstr):
        return optionstr

    def read(self, filenames, encoding='utf8'):
        if isinstance(filenames, (str, os.PathLike)):
            filenames = [filenames]
        read_ok = []
        for filename in filenames:
            try:
                with open(filename, encoding=encoding) as fp:
                    self._read(fp, filename)
            except OSError:
                continue
            if isinstance(filename, os.PathLike):
                filename = os.fspath(filename)
            read_ok.append(filename)
        return read_ok

    def items(self, section=object(), raw=False, vars=None):
        if section is object():
            return super().items()
        d = self._defaults.copy()
        try:
            d.update(self._sections[section])
            d = dict(d)
            for i in d:
                try:
                    value = int(d[i])
                except:
                    value = d[i]
                d[i] = value
            return d
        except KeyError:
            if section != self.default_section:
                raise configparser.NoSectionError(section)


def parse(section, fileName='config.cfg'):
    # parser = ParseConfig()
    # parser.read(fileName)
    # return parser.items(section)
    pass


class Parse(dict):
    crawlConfig = {}
    crawlConfig['shuffle'] = False
    # crawlConfig = parse('crawlConfig')
    # proxyConfig = parse('proxyConfig')
    # dstConfig = parse('dstCon')
    # generateConfig = parse('generateConfig')
    # baseInfo = parse('baseInfo')
    # spyderConfig = parse('spyderConfig')
    # urlConfig = parse('urlConfig')
    # # dstCon = parse('dstCon')
    # srcTable = parse('srcTable')
    # srcCon = parse('srcCon')
    pass