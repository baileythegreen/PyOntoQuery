import optparse
from optparse import TitledHelpFormatter, HelpFormatter, textwrap

class PrettyHelpFormatter (TitledHelpFormatter):
    """Format help with underlined section headers.
    """

    def __init__(self, indent_increment=0, max_help_position=24,
                 width=None, short_first=1):
        self.prog_tag = "%prog"
        HelpFormatter.__init__ (
            self, indent_increment, max_help_position, width, short_first)

    def format_usage(self, usage):
        return "\n%s    %s\n" % (self.format_heading("Usage"), usage)

    def format_heading(self, heading):
        return "%s\n%s\n" % (heading, "=-"[self.level] * len(heading))

    def format_description(self, description):
        if description:
            return "%s%s\n" % (self.format_heading("Description"),
            [self._format_text(line) for line in description] + "\n")
        else:
            return ""

    def _format_text(self, text):
        """
        Format a paragraph of free-form text for inclusion in the
        help output at the current indentation level.
        """
        text_width = max(self.width - self.current_indent, 11)
        indent = "    "
        return textwrap.fill(text,
                             text_width,
                             replace_whitespace=False,
                             drop_whitespace=False,
                             initial_indent=indent,
                             subsequent_indent=indent)

    def format_option(self, option):
        # The help for each option consists of two parts:
        #   * the opt strings and metavars
        #     eg. ("-x", or "-fFILENAME, --file=FILENAME")
        #   * the user-supplied help string
        #     eg. ("turn on expert mode", "read data from FILENAME")
        #
        # If possible, we write both of these on the same line:
        #   -x      turn on expert mode
        #
        # But if the opt string list is too long, we put the help
        # string on a second line, indented to the same column it would
        # start in if it fit on the first line.
        #   -fFILENAME, --file=FILENAME
        #           read data from FILENAME
        result = []
        opts = self.option_strings[option]
        opt_width = self.help_position - self.current_indent - 2
        if len(opts) > opt_width:
            opts = "%*s%s\n" % (self.current_indent, "", opts)
            indent_first = self.help_position
        else:                       # start help on same line as opts
            opts = "%*s%-*s  " % (self.current_indent, "", opt_width, opts)
            indent_first = 0
        result.append(opts)
        if option.help:
            help_text = self.expand_default(option)
            help_text = self.expand_prog(help_text)
            help_lines = textwrap.wrap(help_text, self.help_width,
                replace_whitespace=False, drop_whitespace=False)
            result.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            #result.extend(["%*s%s\n" % (self.help_position, "", line)
            #               for line in help_lines[1:]])
            for line in help_lines[1:]:
                if line.startswith(' '):
                    result.append("%*s%s\n" % (self.help_position, "", line[1:]))
                else:
                    result.append("%*s%s\n" % (self.help_position, "", line))
            result.append("\n")
        elif opts[-1] != "\n":
            result.append("\n")
        return "".join(result)

    def expand_prog(self, option):
        if self.parser is None or not self.prog_tag:
            return option.help
        prog_name = self.parser.get_prog_name()
        return option.help.replace(self.prog_tag, str(prog_name))

    def expand_prog(self, help_text):
        prog_name = self.parser.get_prog_name()
        return help_text.replace(self.prog_tag, str(prog_name))
