/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 08:27:05 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/18 09:43:31 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	int		i;
	char	*search;

	search = NULL;
	i = 0;
	while (s[i])
	{
		if (s[i] == (unsigned char) c)
			search = (char *) &s[i];
		i++;
	}
	if (s[i] == (unsigned char) c)
		search = (char *) &s[i];
	return (search);
}
