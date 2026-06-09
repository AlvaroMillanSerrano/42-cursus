/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 13:46:06 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/19 16:31:52 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

static long int	calc_len(long int l_n)
{
	size_t	len;

	len = 0;
	if (l_n <= 0)
	{
		l_n = -l_n;
		len++;
	}
	while (l_n > 0)
	{
		l_n /= 10;
		len++;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	char		*str;
	size_t		len;
	long int	l_n;

	l_n = n;
	len = calc_len(l_n);
	if (l_n < 0)
		l_n = -l_n;
	str = malloc((len + 1) * sizeof(char));
	if (!str)
		return (NULL);
	str[len] = '\0';
	len--;
	if (l_n == 0)
		str[0] = '0';
	while (l_n > 0)
	{
		str[len] = (l_n % 10) + '0';
		l_n /= 10;
		len--;
	}
	if (n < 0)
		str[0] = '-';
	return (str);
}
