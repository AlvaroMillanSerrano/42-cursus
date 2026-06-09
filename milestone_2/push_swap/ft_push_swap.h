/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_push_swap.h                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 09:27:33 by amillan-          #+#    #+#             */
/*   Updated: 2026/01/07 09:27:35 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PUSH_SWAP_H
# define FT_PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <stdarg.h>

# include <stdio.h>

typedef struct s_stack
{
	int				index;
	int				value;
	struct s_stack	*next;
}	t_stack;

long int	ft_atoi(const char *str);
size_t		ft_strlen(const char *s);
char		*ft_strdup(const char *s1);
char		*ft_substr(char const *s, unsigned int start, size_t len);
int			get_stack_len(t_stack **stack);

int			check_rep(t_stack *argv);
int			check_str(char *argv);
void		clean_error(t_stack **stack_a, t_stack **stack_b);
int			check_is_space_empty(char *argv);
int			check_int(char *argv);

t_stack		*ft_lstnew(int value);
void		ft_lstclear(t_stack **lst);
t_stack		*ft_lstlast(t_stack *lst);
void		ft_lstadd_back(t_stack **lst, t_stack *new);
void		ft_lstadd_front(t_stack **lst, t_stack *new);

void		*ft_free_matrix(char **array, int words);
int			count_words(const char *s, char c);
char		**ft_split(const char *s, char c);

void		push(t_stack **stack_1, t_stack **stack_2);
void		pa(t_stack **stack_a, t_stack **stack_b);
void		pb(t_stack **stack_a, t_stack **stack_b);

void		swap(t_stack **stack);
void		sa(t_stack **stack_a);
void		sb(t_stack **stack_b);
void		ss(t_stack **stack_a, t_stack **stack_b);

void		rotate(t_stack **stack);
void		ra(t_stack **stack_a);
void		rb(t_stack **stack_b);
void		rr(t_stack **stack_a, t_stack **stack_b);

void		reverse_rotate(t_stack **stack);
void		rra(t_stack **stack_a);
void		rrb(t_stack **stack_b);
void		rrr(t_stack **stack_a, t_stack **stack_b);

void		sort(t_stack **stack_a, t_stack **stack_b);

int			get_shortest(t_stack **stack_a);
void		push_shortest(t_stack **stack_a, t_stack **stack_b, int i);
void		push_all_back(t_stack **stack_a, t_stack **stack_b);

int			is_sorted(t_stack *stack_a);
int			fill_stack(char *arg, t_stack **stack_a);

#endif
