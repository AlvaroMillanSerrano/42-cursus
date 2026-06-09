/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/21 11:37:22 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/21 14:38:29 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*n_lst;
	t_list	*n_node;
	void	*content;

	if (!lst || !f || !del)
		return (NULL);
	n_lst = NULL;
	while (lst)
	{
		content = f(lst->content);
		n_node = ft_lstnew(content);
		if (!n_node)
		{
			ft_lstclear(&n_lst, del);
			del(content);
			return (NULL);
		}
		ft_lstadd_back(&n_lst, n_node);
		lst = lst->next;
	}
	return (n_lst);
}
