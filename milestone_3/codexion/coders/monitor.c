/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 12:31:44 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/15 12:31:46 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

static int	check_burnout(t_env *env)
{
	int			i;
	long long	now;
	long long	last_compile;

	i = 0;
	while (i < env->config.num_coders)
	{
		now = get_time_ms();
		pthread_mutex_lock(&env->state_mutex);
		last_compile = env->coders[i].last_compile_start;
		pthread_mutex_unlock(&env->state_mutex);
		if (now - last_compile > env->config.time_burnout)
		{
			pthread_mutex_lock(&env->state_mutex);
			env->simulation_running = 0;
			pthread_mutex_unlock(&env->state_mutex);
			print_status(&env->coders[i], "burned out");
			return (1);
		}
		i++;
	}
	return (0);
}

static int	check_all_compiled(t_env *env)
{
	int	i;
	int	count;
	int	compiles;

	i = 0;
	count = 0;
	while (i < env->config.num_coders)
	{
		pthread_mutex_lock(&env->state_mutex);
		compiles = env->coders[i].compile_count;
		pthread_mutex_unlock(&env->state_mutex);
		if (compiles >= env->config.num_compiles)
			count++;
		i++;
	}
	if (count == env->config.num_coders)
	{
		pthread_mutex_lock(&env->state_mutex);
		env->simulation_running = 0;
		pthread_mutex_unlock(&env->state_mutex);
		return (1);
	}
	return (0);
}

void	*monitor_routine(void *arg)
{
	t_env	*env;

	env = (t_env *)arg;
	while (1)
	{
		if (check_burnout(env))
			break ;
		if (check_all_compiled(env))
			break ;
		usleep(1000);
	}
	return (NULL);
}

int	check_simulation_end(t_env *env)
{
	int	running;

	pthread_mutex_lock(&env->state_mutex);
	running = env->simulation_running;
	pthread_mutex_unlock(&env->state_mutex);
	return (!running);
}
