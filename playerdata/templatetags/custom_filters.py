from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def selectattr(iterable, attr_name, attr_value):
    return [item for item in iterable if getattr(item, attr_name) == attr_value]

@register.filter
def get_team_name(teams, index):
    return teams[index].team_name

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_team_name_by_index(group_teams, index):
    try:
        return group_teams[index]['name']
    except IndexError:
        return ''

@register.filter
def get_grouped_teams(grouped_teams, key):
    return grouped_teams.get(key, [])

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def divide(value, arg):
    return value / arg