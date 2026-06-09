/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 08:38:30 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/13 09:11:11 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	unsigned char	*u_s;
	unsigned char	u_c;
	size_t			i;

	u_s = (unsigned char *) s;
	u_c = (unsigned char) c;
	i = 0;
	while (i < n)
	{
		if (u_s[i] == u_c)
			return (&u_s[i]);
		i++;
	}
	return (NULL);
}
