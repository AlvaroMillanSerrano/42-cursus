/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_push.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 13:09:40 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/09 13:09:41 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

void	push(t_stack **stack_1, t_stack **stack_2)
{
	t_stack	*node_b;

	node_b = *stack_2;
	*stack_2 = node_b->next;
	ft_lstadd_front(stack_1, node_b);
}

void	pa(t_stack **stack_a, t_stack **stack_b)
{
	if (stack_b && *stack_b)
	{
		push(stack_a, stack_b);
		write(1, "pa\n", 3);
	}
}

void	pb(t_stack **stack_a, t_stack **stack_b)
{
	if (stack_a && *stack_a)
	{
		push(stack_b, stack_a);
		write(1, "pb\n", 3);
	}
}
