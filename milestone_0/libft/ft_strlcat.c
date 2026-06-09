/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 13:52:28 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/13 09:12:55 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

size_t	ft_strlcat(char *dest, const char *src, size_t size)
{
	size_t	destlen;
	size_t	srclen;
	size_t	i;

	destlen = 0;
	srclen = ft_strlen(src);
	while (dest[destlen] != '\0' && destlen < size)
		destlen++;
	if (destlen == size)
		return (size + srclen);
	i = 0;
	if (size > 0)
	{
		while (src[i] != '\0' && (destlen + i) < size - 1)
		{
			dest[destlen + i] = src[i];
			i++;
		}
		dest[destlen + i] = '\0';
	}
	return (destlen + srclen);
}
