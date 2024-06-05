from django import template

register = template.Library()


@register.filter()
def mymedia(val):
    if val:
        return f'/media/{val}'

    return 'holder.js/100px225?theme=thumb&bg=55595c&fg=eceeef&text=None'
