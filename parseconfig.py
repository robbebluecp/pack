import configparser
import os


class ParseConfig(configparser.ConfigParser, configparser.NoSectionError):
    def __init__(self, file_name: str):
        """
        parser = parseconfig.ParseConfig('config.cfg')
        print(parser.get_value('name'))
        print(parser.config)
        """
        super(ParseConfig, self).__init__()
        self.read(file_name)
        self.config = {}
        self.init()

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

    def get_value(self, section=object(), raw=False, vars=None):
        return self.items(section=section, raw=raw, vars=vars)

    def init(self):
        for key in self.sections():
            self.config[key] = self.get_value(key)
