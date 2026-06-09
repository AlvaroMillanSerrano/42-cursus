/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 11:45:47 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/02 09:50:44 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_printf.h"

int	ft_puthex(unsigned int n, char *hex)
{
	int	count;

	count = 0;
	if (n >= 16)
		count = ft_puthex((n / 16), hex);
	count += ft_putchar((hex[n % 16]));
	return (count);
}
