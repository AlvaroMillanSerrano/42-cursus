/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 09:48:27 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/02 12:23:27 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_printf.h"

static int	convert_format(va_list args, char ch)
{
	if (ch == 'c')
		return (ft_putchar(va_arg(args, int)));
	else if (ch == 's')
		return (ft_putstr(va_arg(args, char *)));
	else if (ch == 'p')
		return (ft_putvoid((unsigned long int)va_arg(args, void *)));
	else if (ch == 'd')
		return (ft_putnbr(va_arg(args, int), 0));
	else if (ch == 'i')
		return (ft_putnbr(va_arg(args, int), 0));
	else if (ch == 'u')
		return (ft_putunsig(va_arg(args, unsigned int), 0));
	else if (ch == 'x')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789abcdef"));
	else if (ch == 'X')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789ABCDEF"));
	else if (ch == '%')
		return (ft_putchar('%'));
	else
		return (0);
}

int	ft_printf(const char *format, ...)
{
	int		i;
	int		count;
	va_list	args;

	va_start(args, format);
	i = 0;
	count = 0;
	while (format[i])
	{
		if (format[i] == '%')
		{
			if (format[i + 1])
			{
				count += convert_format(args, format[i + 1]);
				i += 2;
			}
			else
				return (count);
		}
		else
		{
			write(1, &format[i], 1);
			count++;
			i++;
		}
	}
	va_end(args);
	return (count);
}
