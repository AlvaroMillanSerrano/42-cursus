/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_push_swap_utils.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 09:27:09 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/07 09:27:11 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

long int	ft_atoi(const char *str)
{
	int			i;
	int			j;
	long int	result;

	i = 0;
	result = 0;
	j = 1;
	while (str[i] == 32 || (str[i] >= 9 && str[i] <= 13))
		i++;
	if (str[i] == '-' || str[i] == '+')
	{
		if (str[i] == '-')
			j = -j;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		result = (result * 10) + (str[i] - '0');
		i++;
	}
	return (result * j);
}

size_t	ft_strlen(const char *s)
{
	size_t	result;

	result = 0;
	while (s[result])
	{
		result++;
	}
	return (result);
}

char	*ft_strdup(const char *s1)
{
	char	*dest;
	int		i;

	i = 0;
	while (s1[i])
		i++;
	dest = malloc(i + 1 * sizeof(char));
	if (!dest)
		return (NULL);
	i = 0;
	while (s1[i])
	{
		dest[i] = s1[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*dest;
	size_t	i;
	size_t	s_len;

	if (!s)
		return (NULL);
	s_len = ft_strlen(s);
	if (start >= s_len)
		return (ft_strdup(""));
	if (len > ft_strlen(s + start))
		len = ft_strlen(s + start);
	dest = malloc((len + 1) * sizeof(char));
	if (!dest)
		return (NULL);
	i = 0;
	while (i < len)
	{
		dest[i] = s[start + i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

int	get_stack_len(t_stack **stack)
{
	t_stack	*node;
	int		i;

	node = *stack;
	i = 1;
	while (node->next)
	{
		node = node->next;
		i++;
	}
	return (i);
}
