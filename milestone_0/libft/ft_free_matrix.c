/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_free_matrix.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/19 15:09:51 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/19 15:12:35 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

void	*ft_free_matrix(char **array, int words)
{
	int	i;

	i = 0;
	while (i < words)
	{
		free(array[i]);
		i++;
	}
	free(array);
	return (NULL);
}
