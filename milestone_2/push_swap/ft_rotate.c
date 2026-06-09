/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_rotate.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 13:20:52 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/09 13:20:55 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

void	rotate(t_stack **stack)
{
	t_stack	*node_f;
	t_stack	*node_l;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	node_f = *stack;
	node_l = ft_lstlast(*stack);
	*stack = (*stack)->next;
	node_f->next = NULL;
	node_l->next = node_f;
}

void	ra(t_stack **stack_a)
{
	rotate(stack_a);
	write(1, "ra\n", 3);
}

void	rb(t_stack **stack_b)
{
	rotate(stack_b);
	write(1, "rb\n", 3);
}

void	rr(t_stack **stack_a, t_stack **stack_b)
{
	rotate(stack_a);
	rotate(stack_b);
	write(1, "rr\n", 3);
}
