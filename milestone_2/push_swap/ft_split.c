/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 10:15:54 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/09 10:15:56 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_push_swap.h"

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

int	count_words(const char *s, char c)
{
	int	i;
	int	word_count;

	i = 0;
	word_count = 0;
	while (s[i])
	{
		if (s[i] != c && (i == 0 || s[i - 1] == c))
			word_count++;
		i++;
	}
	return (word_count);
}

static char	*fill_word(const char *s, int start, int end)
{
	char	*word;

	word = ft_substr(s, start, (end - start));
	return (word);
}

static char	**create_array(const char *s, char c, char **array, int del)
{
	int	c_let;
	int	c_word;

	c_let = 0;
	c_word = 0;
	while (c_let <= (int)ft_strlen(s) && c_word < count_words(s, c))
	{
		if (del < 0 && s[c_let] != c)
		{
			del = c_let;
		}
		else if ((s[c_let] == c || c_let == (int)ft_strlen(s)) && del >= 0)
		{
			array[c_word] = fill_word(s, del, c_let);
			if (array[c_word] == NULL)
				return (ft_free_matrix(array, c_word));
			c_word++;
			del = -1;
		}
		c_let++;
	}
	array[c_word] = NULL;
	return (array);
}

char	**ft_split(const char *s, char c)
{
	char	**array;

	array = malloc((count_words(s, c) + 1) * sizeof(char *));
	if (!array)
		return (NULL);
	array = create_array(s, c, array, -1);
	return (array);
}
