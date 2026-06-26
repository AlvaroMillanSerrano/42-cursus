/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/10 12:27:02 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/10 12:27:13 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

static int	compare_requests(t_request a, t_request b, int mode)
{
	if (mode == 2)
	{
		if (a.deadline != b.deadline)
			return (a.deadline < b.deadline);
	}
	if (a.request_time != b.request_time)
		return (a.request_time < b.request_time);
	return (a.coder_id < b.coder_id);
}

void	heap_push(t_heap *heap, t_request req, int mode)
{
	int			i;
	int			parent;
	t_request	tmp;

	i = heap->size;
	heap->requests[i] = req;
	heap->size++;
	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (compare_requests(heap->requests[i], heap->requests[parent], mode))
		{
			tmp = heap->requests[i];
			heap->requests[i] = heap->requests[parent];
			heap->requests[parent] = tmp;
			i = parent;
		}
		else
			break ;
	}
}

static void	down_heap(t_heap *heap, int i, int mode)
{
	int			left;
	int			smallest;
	t_request	tmp;

	while (1)
	{
		left = (2 * i) + 1;
		smallest = i;
		if (left < heap->size && compare_requests(heap->requests[left],
				heap->requests[smallest], mode))
			smallest = left;
		if (left + 1 < heap->size && compare_requests(heap->requests[left + 1],
				heap->requests[smallest], mode))
			smallest = left + 1;
		if (smallest == i)
			break ;
		tmp = heap->requests[i];
		heap->requests[i] = heap->requests[smallest];
		heap->requests[smallest] = tmp;
		i = smallest;
	}
}

t_request	heap_pop(t_heap *heap, int mode)
{
	t_request	root;

	root = heap->requests[0];
	heap->size--;
	if (heap->size > 0)
	{
		heap->requests[0] = heap->requests[heap->size];
		down_heap(heap, 0, mode);
	}
	return (root);
}
