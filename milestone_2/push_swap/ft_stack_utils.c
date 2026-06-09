/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_stack_utils.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 09:27:47 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/07 09:27:49 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

t_stack	*ft_lstnew(int value)
{
	t_stack	*new_stack;

	new_stack = malloc(sizeof(t_stack));
	if (!new_stack)
		return (NULL);
	new_stack->value = value;
	new_stack->next = NULL;
	return (new_stack);
}

void	ft_lstclear(t_stack **lst)
{
	t_stack	*c_node;
	t_stack	*n_node;

	c_node = *lst;
	if (!c_node)
		return ;
	while (c_node)
	{
		n_node = c_node->next;
		free(c_node);
		c_node = n_node;
	}
	*lst = NULL;
}

void	ft_lstadd_front(t_stack **lst, t_stack *new)
{
	new->next = *lst;
	*lst = new;
}

t_stack	*ft_lstlast(t_stack *lst)
{
	t_stack	*temp;

	temp = lst;
	if (!temp)
		return (NULL);
	while (temp->next)
		temp = temp->next;
	return (temp);
}

void	ft_lstadd_back(t_stack **lst, t_stack *new)
{
	t_stack	*last_node;

	last_node = ft_lstlast(*lst);
	if (!last_node)
		*lst = new;
	else
	{
		last_node = ft_lstlast(*lst);
		last_node->next = new;
	}
}
