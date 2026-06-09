/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/21 10:00:45 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/21 11:02:48 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

void	ft_lstclear(t_list **lst, void (*del)(void*))
{
	t_list	*c_node;
	t_list	*n_node;

	c_node = *lst;
	if (!c_node || !del)
		return ;
	while (c_node)
	{
		n_node = c_node->next;
		ft_lstdelone(c_node, del);
		c_node = n_node;
	}
	*lst = NULL;
}
