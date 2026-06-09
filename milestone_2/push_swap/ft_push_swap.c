/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_push_swap.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 09:27:22 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/07 09:27:23 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

void	clear_nodes(t_stack **stack_a, t_stack **stack_b)
{
	ft_lstclear(stack_a);
	ft_lstclear(stack_b);
	*stack_a = NULL;
	*stack_b = NULL;
}

int	add_node(t_stack **stack_a, int value)
{
	t_stack	*n_node;

	n_node = ft_lstnew(value);
	if (!n_node)
		return (1);
	ft_lstadd_back(stack_a, n_node);
	return (0);
}

void	clean_error(t_stack **stack_a, t_stack **stack_b)
{
	ft_lstclear(stack_a);
	ft_lstclear(stack_b);
	write(1, "Error\n", 6);
}

int	fill_stack(char *arg, t_stack **stack_a)
{
	char		**words;
	int			word_count;
	int			current_word;
	int			i;

	words = ft_split(arg, ' ');
	i = 0;
	current_word = 0;
	word_count = count_words(arg, ' ');
	while (words[i])
	{
		if ((check_str(words[i])))
			return (ft_free_matrix(words, word_count), 1);
		else if (check_int(words[i]))
			return (ft_free_matrix(words, word_count), 1);
		else if (add_node(stack_a, (int)ft_atoi(words[i])))
			return (ft_free_matrix(words, word_count), 1);
		current_word++;
		i++;
	}
	return (ft_free_matrix(words, word_count), 0);
}

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	int		i;

	if (argc < 2)
		return (0);
	stack_a = NULL;
	stack_b = NULL;
	i = 1;
	while (argv[i])
	{
		if (check_is_space_empty(argv[i]))
		{
			return (clean_error(&stack_a, &stack_b), 0);
		}
		if (fill_stack(argv[i], &stack_a))
			return (clean_error(&stack_a, &stack_b), 0);
		i++;
	}
	if ((check_rep(stack_a)))
		return (clean_error(&stack_a, &stack_b), 0);
	sort(&stack_a, &stack_b);
	clear_nodes(&stack_a, &stack_b);
	return (0);
}
