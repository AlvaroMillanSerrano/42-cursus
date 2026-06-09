/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 10:51:13 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/02 09:06:16 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_printf.h"

int	ft_putnbr(int n, int count)
{
	long int	l_n;

	l_n = n;
	if (l_n < 0)
	{
		write(1, "-", 1);
		l_n = -l_n;
		count++;
	}
	if (l_n >= 10)
	{
		count = ft_putnbr((l_n / 10), count);
	}
	count += ft_putchar((l_n % 10 + '0'));
	return (count);
}
