/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 11:16:47 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/18 12:37:30 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

static void	move_data(char *c_dest, const char *c_src, size_t n)
{
	size_t	i;

	i = 0;
	if (c_dest > c_src)
	{
		while (n > 0)
		{
			n--;
			c_dest[n] = c_src[n];
		}
	}
	else
	{
		while (i < n)
		{
			c_dest[i] = c_src[i];
			i++;
		}
	}
}

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	char		*c_dest;
	const char	*c_src;

	if (src == NULL && dest == NULL)
		return (NULL);
	c_dest = dest;
	c_src = src;
	move_data(c_dest, c_src, n);
	return (dest);
}
