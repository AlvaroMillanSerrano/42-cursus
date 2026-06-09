/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 12:28:49 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/28 12:59:23 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_printf.h"

int	ft_putstr(char *s)
{
	int	i;
	int	count;

	if (!s)
		s = "(null)";
	i = 0;
	count = 0;
	while (s[i])
	{
		write(1, &s[i], 1);
		count++;
		i++;
	}
	return (count);
}
