from argparse import ArgumentParser
import os

from docutils import nodes
from docutils.parsers.rst.directives import flag, unchanged
from sphinx.util.compat import Directive
from sphinx.util.nodes import nested_parse_with_titles

from sphinxarg.parser import parse_parser, parser_navigate


def map_nested_definitions(nested_content):
    if nested_content is None:
        raise Exception('Nested content should be iterable, not null')
    # build definition dictionary
    definitions = {}
    for item in nested_content:
        if not isinstance(item, nodes.definition_list):
            continue
        for subitem in item:
            if not isinstance(subitem, nodes.definition_list_item):
                continue
            if not len(subitem.children) > 0:
                continue
            classifier = '@after'
            idx = subitem.first_child_matching_class(nodes.classifier)
            if idx is not None:
                ci = subitem[idx]
                if len(ci.children) > 0:
                    classifier = ci.children[0].astext()
            if classifier is not None and classifier not in (
                    '@replace', '@before', '@after'):
                raise Exception('Unknown classifier: %s' % classifier)
            idx = subitem.first_child_matching_class(nodes.term)
            if idx is not None:
                ch = subitem[idx]
                if len(ch.children) > 0:
                    term = ch.children[0].astext()
                    idx = subitem.first_child_matching_class(nodes.definition)
                    if idx is not None:
                        def_node = subitem[idx]
                        def_node.attributes['classifier'] = classifier
                        definitions[term] = def_node
    return definitions


def print_arg_list(data, nested_content):
    definitions = map_nested_definitions(nested_content)
    items = []
    if 'args' in data:
        for arg in data['args']:
            my_def = [nodes.paragraph(text=arg['help'])] if arg['help'] else []
            name = arg['name']
            my_def = apply_definition(definitions, my_def, name)
            if len(my_def) == 0:
                my_def.append(nodes.paragraph(text='Undocumented'))
            if 'choices' in arg:
                my_def.append(nodes.paragraph(
                    text=('Possible choices: %s' % ', '.join([str(c) for c in arg['choices']]))))
            items.append(
                nodes.option_list_item(
                    '', nodes.option_group('', nodes.option_string(text=name)),
                    nodes.description('', *my_def)))
    return nodes.option_list('', *items) if items else None


def print_opt_list(data, nested_content):
    definitions = map_nested_definitions(nested_content)
    items = []
    if 'options' in data:
        for opt in data['options']:
            names = []
            my_def = [nodes.paragraph(text=opt['help'])] if opt['help'] else []
            for name in opt['name']:
                option_declaration = [nodes.option_string(text=name)]
                if opt['default'] is not None \
                        and opt['default'] != '==SUPPRESS==':
                    option_declaration += nodes.option_argument(
                        '', text='=' + str(opt['default']))
                names.append(nodes.option('', *option_declaration))
                my_def = apply_definition(definitions, my_def, name)
            if len(my_def) == 0:
                my_def.append(nodes.paragraph(text='Undocumented'))
            if 'choices' in opt:
                my_def.append(nodes.paragraph(
                    text=('Possible choices: %s' % ', '.join([str(c) for c in opt['choices']]))))
            items.append(
                nodes.option_list_item(
                    '', nodes.option_group('', *names),
                    nodes.description('', *my_def)))
    return nodes.option_list('', *items) if items else None


def print_command_args_and_opts(arg_list, opt_list, sub_list=None):
    items = []
    if arg_list:
        items.append(nodes.definition_list_item(
            '', nodes.term(text='Positional arguments:'),
            nodes.definition('', arg_list)))
    if opt_list:
        items.append(nodes.definition_list_item(
            '', nodes.term(text='Options:'),
            nodes.definition('', opt_list)))
    if sub_list and len(sub_list):
        items.append(nodes.definition_list_item(
            '', nodes.term(text='Sub-commands:'),
            nodes.definition('', sub_list)))
    return nodes.definition_list('', *items)


def apply_definition(definitions, my_def, name):
    if name in definitions:
        definition = definitions[name]
        classifier = definition['classifier']
        if classifier == '@replace':
            return definition.children
        if classifier == '@after':
            return my_def + definition.children
        if classifier == '@before':
            return definition.children + my_def
        raise Exception('Unknown classifier: %s' % classifier)
    return my_def


def print_subcommand_list(data, nested_content):
    definitions = map_nested_definitions(nested_content)
    items = []
    if 'children' in data:
        for child in data['children']:
            my_def = [nodes.paragraph(
                text=child['help'])] if child['help'] else []
            name = child['name']
            my_def = apply_definition(definitions, my_def, name)
            if len(my_def) == 0:
                my_def.append(nodes.paragraph(text='Undocumented'))
            my_def.append(nodes.literal_block(text=child['usage']))
            my_def.append(print_command_args_and_opts(
                print_arg_list(child, nested_content),
                print_opt_list(child, nested_content)
            ))
            items.append(
                nodes.definition_list_item(
                    '',
                    nodes.term('', '', nodes.strong(text=name)),
                    nodes.definition('', *my_def)
                )
            )
    return nodes.definition_list('', *items)


class ArgParseDirective(Directive):
    has_content = True
    option_spec = dict(module=unchanged, func=unchanged, ref=unchanged,
                       prog=unchanged, path=unchanged, nodefault=flag,
                       manpage=unchanged, nosubcommands=unchanged)

    def _construct_manpage_specific_structure(self, parser_info):
        """
        Construct a typical man page consisting of the following elements:
            NAME (automatically generated, out of our control)
            SYNOPSIS
            DESCRIPTION
            OPTIONS
            FILES
            SEE ALSO
            BUGS
        """
        # SYNOPSIS section
        synopsis_section = nodes.section(
            '',
            nodes.title(text='Synopsis'),
            nodes.literal_block(text=parser_info["bare_usage"]),
            ids=['synopsis-section'])
        # DESCRIPTION section
        description_section = nodes.section(
            '',
            nodes.title(text='Description'),
            nodes.paragraph(text=parser_info.get(
                'description', parser_info.get(
                    'help', "undocumented").capitalize())),
            ids=['description-section'])
        nested_parse_with_titles(
            self.state, self.content, description_section)
        if parser_info.get('epilog'):
            # TODO: do whatever sphinx does to understand ReST inside
            # docstrings magically imported from other places. The nested
            # parse method invoked above seem to be able to do this but
            # I haven't found a way to do it for arbitrary text
            description_section += nodes.paragraph(
                text=parser_info['epilog'])
        # OPTIONS section
        options_section = nodes.section(
            '',
            nodes.title(text='Options'),
            ids=['options-section'])
        if 'args' in parser_info:
            options_section += nodes.paragraph()
            options_section += nodes.subtitle(text='Positional arguments:')
            options_section += self._format_positional_arguments(parser_info)
        if 'options' in parser_info:
            options_section += nodes.paragraph()
            options_section += nodes.subtitle(text='Optional arguments:')
            options_section += self._format_optional_arguments(parser_info)
        items = [
            # NOTE: we cannot generate NAME ourselves. It is generated by
            # docutils.writers.manpage
            synopsis_section,
            description_section,
            # TODO: files
            # TODO: see also
            # TODO: bugs
        ]
        if len(options_section.children) > 1:
            items.append(options_section)
        if 'nosubcommands' not in self.options:
            # SUBCOMMANDS section (non-standard)
            subcommands_section = nodes.section(
                '',
                nodes.title(text='Sub-Commands'),
                ids=['subcommands-section'])
            if 'children' in parser_info:
                subcommands_section += self._format_subcommands(parser_info)
            if len(subcommands_section) > 1:
                items.append(subcommands_section)
        if os.getenv("INCLUDE_DEBUG_SECTION"):
            import json
            # DEBUG section (non-standard)
            debug_section = nodes.section(
                '',
                nodes.title(text="Argparse + Sphinx Debugging"),
                nodes.literal_block(text=json.dumps(parser_info, indent='  ')),
                ids=['debug-section'])
            items.append(debug_section)
        return items

    def _format_positional_arguments(self, parser_info):
        assert 'args' in parser_info
        items = []
        for arg in parser_info['args']:
            arg_items = []
            if arg['help']:
                arg_items.append(nodes.paragraph(text=arg['help']))
            else:
                arg_items.append(nodes.paragraph(text='Undocumented'))
            if 'choices' in arg:
                arg_items.append(
                    nodes.paragraph(
                        text='Possible choices: ' + ', '.join(arg['choices'])))
            items.append(
                nodes.option_list_item(
                    '', nodes.option_group(
                        '', nodes.description(text=arg['metavar'])),
                    nodes.description('', *arg_items)))
        return nodes.option_list('', *items)

    def _format_optional_arguments(self, parser_info):
        assert 'options' in parser_info
        items = []
        for opt in parser_info['options']:
            names = []
            opt_items = []
            for name in opt['name']:
                option_declaration = [nodes.option_string(text=name)]
                if opt['default'] is not None \
                        and opt['default'] != '==SUPPRESS==':
                    option_declaration += nodes.option_argument(
                        '', text='=' + str(opt['default']))
                names.append(nodes.option('', *option_declaration))
            if opt['help']:
                opt_items.append(nodes.paragraph(text=opt['help']))
            else:
                opt_items.append(nodes.paragraph(text='Undocumented'))
            if 'choices' in opt:
                opt_items.append(
                    nodes.paragraph(
                        text='Possible choices: ' + ', '.join(opt['choices'])))
            items.append(
                nodes.option_list_item(
                    '', nodes.option_group('', *names),
                    nodes.description('', *opt_items)))
        return nodes.option_list('', *items)

    def _format_subcommands(self, parser_info):
        assert 'children' in parser_info
        items = []
        for subcmd in parser_info['children']:
            subcmd_items = []
            if subcmd['help']:
                subcmd_items.append(nodes.paragraph(text=subcmd['help']))
            else:
                subcmd_items.append(nodes.paragraph(text='Undocumented'))
            items.append(
                nodes.definition_list_item(
                    '',
                    nodes.term('', '', nodes.strong(
                        text=subcmd['bare_usage'])),
                    nodes.definition('', *subcmd_items)))
        return nodes.definition_list('', *items)

    def run(self):
        if 'module' in self.options and 'func' in self.options:
            module_name = self.options['module']
            attr_name = self.options['func']
        elif 'ref' in self.options:
            _parts = self.options['ref'].split('.')
            module_name = '.'.join(_parts[0:-1])
            attr_name = _parts[-1]
        else:
            raise self.error(
                ':module: and :func: should be specified, or :ref:')
        mod = __import__(module_name, globals(), locals(), [attr_name])
        if not hasattr(mod, attr_name):
            raise self.error((
                'Module "%s" has no attribute "%s"\n'
                'Incorrect argparse :module: or :func: values?'
            ) % (module_name, attr_name))
        func = getattr(mod, attr_name)
        if isinstance(func, ArgumentParser):
            parser = func
        else:
            parser = func()
        if 'path' not in self.options:
            self.options['path'] = ''
        path = str(self.options['path'])
        if 'prog' in self.options:
            parser.prog = self.options['prog']
        result = parse_parser(
            parser, skip_default_values='nodefault' in self.options)
        result = parser_navigate(result, path)
        if 'manpage' in self.options:
            return self._construct_manpage_specific_structure(result)
        nested_content = nodes.paragraph()
        self.state.nested_parse(
            self.content, self.content_offset, nested_content)
        nested_content = nested_content.children
        items = []
        # add common content between
        for item in nested_content:
            if not isinstance(item, nodes.definition_list):
                items.append(item)
        if 'description' in result:
            items.append(nodes.paragraph(text=result['description']))
        items.append(nodes.literal_block(text=result['usage']))
        items.append(print_command_args_and_opts(
            print_arg_list(result, nested_content),
            print_opt_list(result, nested_content),
            print_subcommand_list(result, nested_content)
        ))
        if 'epilog' in result:
            items.append(nodes.paragraph(text=result['epilog']))
        return items


def setup(app):
    app.add_directive('argparse', ArgParseDirective)
