/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunsig.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 10:59:23 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/02 09:36:54 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_printf.h"

int	ft_putunsig(unsigned int n, int count)
{
	size_t	l_n;

	l_n = n;
	if (l_n >= 10)
	{
		count = ft_putunsig((l_n / 10), count);
	}
	count += ft_putchar((l_n % 10 + '0'));
	return (count);
}
