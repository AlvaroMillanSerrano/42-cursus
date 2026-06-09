/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_reverse_rotate.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 13:21:12 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/09 13:21:13 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

void	reverse_rotate(t_stack **stack)
{
	t_stack	*node_f;
	t_stack	*node_l;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	node_f = *stack;
	node_l = ft_lstlast(*stack);
	while (node_f->next->next)
		node_f = node_f->next;
	node_f->next = NULL;
	node_l->next = *stack;
	*stack = node_l;
}

void	rra(t_stack **stack_a)
{
	reverse_rotate(stack_a);
	write(1, "rra\n", 4);
}

void	rrb(t_stack **stack_b)
{
	reverse_rotate(stack_b);
	write(1, "rrb\n", 4);
}

void	rrr(t_stack **stack_a, t_stack **stack_b)
{
	reverse_rotate(stack_a);
	reverse_rotate(stack_b);
	write(1, "rrr\n", 4);
}
