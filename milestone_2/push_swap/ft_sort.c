/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 12:04:21 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/14 12:04:23 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

void	assign_indexes(t_stack *stack_a)
{
	t_stack	*current;
	t_stack	*comp;
	int		index;

	current = stack_a;
	while (current)
	{
		index = 0;
		comp = stack_a;
		while (comp)
		{
			if (comp->value < current->value)
				index++;
			comp = comp->next;
		}
		current->index = index;
		current = current->next;
	}
}

void	sort_3(t_stack **stack_a)
{
	int	f_node;
	int	s_node;
	int	t_node;

	f_node = (*stack_a)->index;
	s_node = (*stack_a)->next->index;
	t_node = (*stack_a)->next->next->index;
	if (f_node > s_node && f_node < t_node)
		sa(stack_a);
	else if (f_node > s_node && s_node > t_node)
	{
		sa(stack_a);
		rra(stack_a);
	}
	else if (f_node < s_node && f_node > t_node)
		rra(stack_a);
	else if (f_node > s_node && s_node < t_node && f_node > t_node)
		ra(stack_a);
	else if (f_node < s_node && s_node > t_node && f_node < t_node)
	{
		sa(stack_a);
		ra(stack_a);
	}
}

void	sort_4_5(t_stack **stack_a, t_stack **stack_b, int len)
{
	int	i;

	if (len == 5)
	{
		i = get_shortest(stack_a);
		push_shortest(stack_a, stack_b, i);
		i = get_shortest(stack_a);
		push_shortest(stack_a, stack_b, i);
		sort_3(stack_a);
		pa(stack_a, stack_b);
		pa(stack_a, stack_b);
	}
	else
	{
		i = get_shortest(stack_a);
		push_shortest(stack_a, stack_b, i);
		sort_3(stack_a);
		pa(stack_a, stack_b);
	}
}

void	sort_chunks(t_stack **stack_a, t_stack **stack_b, int len)
{
	int	i;
	int	range;

	if (len <= 100)
		range = len / 6;
	else
		range = len / 12;
	i = 0;
	while (*stack_a)
	{
		if ((*stack_a)->index <= i)
		{
			pb(stack_a, stack_b);
			rb(stack_b);
			i++;
		}
		else if ((*stack_a)->index <= i + range)
		{
			pb(stack_a, stack_b);
			i++;
		}
		else
			ra(stack_a);
	}
	push_all_back(stack_a, stack_b);
}

void	sort(t_stack **stack_a, t_stack **stack_b)
{
	int	stack_len;

	stack_len = get_stack_len(stack_a);
	assign_indexes(*stack_a);
	if (is_sorted(*stack_a))
		return ;
	if (stack_len == 2)
	{
		if ((*stack_a)->value > (*stack_a)->next->value)
			sa(stack_a);
	}
	else if (stack_len == 3)
		sort_3(stack_a);
	else if (stack_len == 4 || stack_len == 5)
		sort_4_5(stack_a, stack_b, stack_len);
	else
		sort_chunks(stack_a, stack_b, stack_len);
}
