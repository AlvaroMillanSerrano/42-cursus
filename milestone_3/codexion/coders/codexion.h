/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/10 09:35:12 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/10 09:35:23 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#ifndef CODEXION_H
# define CODEXION_H

# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <pthread.h>
# include <sys/time.h>
# include <unistd.h>

typedef struct s_config
{
	int	num_coders;
	int	time_burnout;
	int	time_compile;
	int	time_debug;
	int	time_refactor;
	int	num_compiles;
	int	cooldown;
	int	scheduler_mode;
}	t_config;

struct	s_env;

typedef struct s_coder
{
	int				id;
	int				compile_count;
	long long		last_compile_start;
	pthread_t		thread;
	int				left_dongle;
	int				right_dongle;
	struct s_env	*env;
}	t_coder;

typedef struct s_request
{
	int			coder_id;
	long long	request_time;
	long long	deadline;
}	t_request;

typedef struct s_heap
{
	t_request	*requests;
	int			size;
}	t_heap;

typedef struct s_dongle
{
	int				id;
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	int				is_taken;
	int				holding_coder;
	long long		available_at;
	t_heap			queue;
}	t_dongle;

typedef struct s_env
{
	t_config		config;
	t_coder			*coders;
	t_dongle		*dongles;
	long long		start_time;
	int				simulation_running;
	pthread_mutex_t	state_mutex;
	pthread_mutex_t	log_mutex;
}	t_env;

int			parse_args(t_config *config, int argc, char **argv);
int			init_env(t_env *env);
void		free_env(t_env *env);
void		heap_push(t_heap *heap, t_request req, int mode);
t_request	heap_pop(t_heap *heap, int mode);
void		take_single_dongle(t_coder *coder, t_dongle *dongle);
void		release_single_dongle(t_coder *coder, t_dongle *dongle);
void		smart_sleep(long long ms, t_env *env);

long long	get_time_ms(void);
void		print_status(t_coder *coder, const char *status);
void		*coder_routine(void *arg);
void		*monitor_routine(void *arg);
int			is_sim_over(t_coder *coder);
int			try_acquire_both(t_coder *coder, t_dongle *left, t_dongle *right);
void		execute_compile_cycle(t_coder *coder);
int			check_simulation_end(t_env *env);
void		check_and_stop_simulation(t_coder *coder);
int			can_acquire(t_coder *coder, t_dongle *left, t_dongle *right,
				long long now);
void		lock_dongles_ordered(t_dongle *left, t_dongle *right);

#endif
