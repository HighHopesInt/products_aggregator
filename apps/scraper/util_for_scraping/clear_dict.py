from django.contrib import messages


def clear(dictionary, request):
    try:
        for value in dictionary.values():
            del value[:]
    except TypeError:
        return messages.error(request, 'What\' wrong')
