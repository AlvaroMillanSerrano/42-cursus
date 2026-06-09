/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_check_errors.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 10:45:15 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/07 10:45:17 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "ft_push_swap.h"

int	is_sorted(t_stack *stack_a)
{
	while (stack_a && stack_a->next)
	{
		if (stack_a->value > stack_a->next->value)
			return (0);
		stack_a = stack_a->next;
	}
	return (1);
}

int	check_is_space_empty(char *argv)
{
	int	i;

	i = 0;
	while (argv[i])
	{
		if (argv[i] != ' ' && !(argv[i] >= 9 && argv[i] <= 13))
			return (0);
		i++;
	}
	return (1);
}

int	check_rep(t_stack *a)
{
	t_stack		*del;
	t_stack		*comp;

	del = a;
	while (del)
	{
		comp = del->next;
		while (comp)
		{
			if (del->value == comp->value)
				return (1);
			comp = comp->next;
		}
		del = del->next;
	}
	return (0);
}

int	check_str(char *argv)
{
	int		i;

	i = 0;
	if (argv[i] == '-' || argv[i] == '+')
		i++;
	while (argv[i])
	{
		if (argv[i] < '0' || argv[i] > '9' )
			return (1);
		i++;
	}
	return (0);
}

int	check_int(char *argv)
{
	long int	num;

	num = ft_atoi(argv);
	if (num > -2147483648 && num < 2147483647)
		return (0);
	return (1);
}
