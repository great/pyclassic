import locale

locale.setlocale(locale.LC_ALL, '')


def formatted(num):
	return locale.format('%d', num, True)

