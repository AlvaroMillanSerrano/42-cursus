/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/19 13:26:14 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/19 13:26:17 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

int	get_index_pos(t_stack *stack, int target_index)
{
	int	pos;

	pos = 0;
	while (stack)
	{
		if (stack->index == target_index)
			return (pos);
		stack = stack->next;
		pos++;
	}
	return (-1);
}

int	get_max_index(t_stack *stack)
{
	int	max;

	max = stack->index;
	while (stack)
	{
		if (stack->index > max)
			max = stack->index;
		stack = stack->next;
	}
	return (max);
}

int	get_shortest(t_stack **stack_a)
{
	t_stack	*c_node;
	int		min;
	int		c_pos;
	int		i;

	c_node = *stack_a;
	min = c_node->index;
	c_pos = 0;
	i = 0;
	while (c_node)
	{
		if (c_node->index < min)
		{
			min = c_node->index;
			c_pos = i;
		}
		c_node = c_node->next;
		i++;
	}
	return (c_pos);
}

void	push_shortest(t_stack **stack_a, t_stack **stack_b, int i)
{
	int	len;

	len = get_stack_len(stack_a);
	if (i <= len / 2)
	{
		while (i > 0)
		{
			ra(stack_a);
			i--;
		}
	}
	else
	{
		while (i < len - 1)
		{
			rra(stack_a);
			i++;
		}
	}
	pb(stack_a, stack_b);
}

void	push_all_back(t_stack **stack_a, t_stack **stack_b)
{
	int	len;
	int	p_index;
	int	max_index;

	while (*stack_b)
	{
		len = get_stack_len(stack_b);
		max_index = get_max_index(*stack_b);
		p_index = get_index_pos(*stack_b, max_index);
		if (p_index <= len / 2)
		{
			while ((*stack_b)->index != max_index)
				rb(stack_b);
		}
		else
		{
			while ((*stack_b)->index != max_index)
				rrb(stack_b);
		}
		pa(stack_a, stack_b);
	}
}
