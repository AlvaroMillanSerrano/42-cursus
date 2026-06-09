/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putvoid.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 12:52:56 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/02 09:51:38 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_printf.h"

static int	puthex(unsigned long int n, char *hex)
{
	int	count;

	count = 0;
	if (n >= 16)
		count = puthex((n / 16), hex);
	count += ft_putchar((hex[n % 16]));
	return (count);
}

int	ft_putvoid(unsigned long int ptr)
{
	if (!ptr)
		return (ft_putstr("(nil)"));
	return (ft_putstr("0x") + puthex(ptr, "0123456789abcdef"));
}
