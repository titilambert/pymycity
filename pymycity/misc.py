import pprint


def cli_helper(parser, cities):
    help_data = {"Cities": {}}
    for city_name in sorted(cities):
        help_data["Cities"][city_name] = {}
        for command in cities[city_name].commands:
            command_help = command.parser.format_help().replace(command.parser.format_usage(), "").strip("\n")
            #command_help = command.parser.format_help().strip("\n")
            help_data["Cities"][city_name][command.name] = command.help

    messages = []
    for title, cities_data in help_data.items():
        msg = "{}:".format(title)
        messages.append(msg)
        for city_name, city_commands in cities_data.items():
            msg = "    * {}:".format(city_name)
            messages.append(msg)
            for command_name, command_help in city_commands.items():
                msg = "        + {}:".format(command_name)
                messages.append(msg)
                messages.append("            - {}".format(command_help))
    parser.print_usage()
    print("\n")
    print("\n".join(messages))
