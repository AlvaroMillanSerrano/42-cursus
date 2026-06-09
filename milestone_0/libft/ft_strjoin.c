/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 09:22:14 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/13 12:48:04 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*join;
	size_t	l_s1;
	size_t	l_s2;

	if (!s1 || !s2)
		return (NULL);
	l_s1 = ft_strlen(s1);
	l_s2 = ft_strlen(s2);
	join = malloc((l_s1 + l_s2 + 1) * sizeof(char));
	if (join == NULL)
		return (NULL);
	ft_strlcpy(join, s1, (l_s1 + 1));
	ft_strlcat(join, s2, (l_s1 + l_s2 +1));
	return (join);
}
