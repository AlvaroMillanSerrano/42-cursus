/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   actions.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 12:05:55 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/11 12:05:57 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

void	free_env(t_env *env)
{
	int	i;

	if (!env)
		return ;
	if (env->dongles)
	{
		i = 0;
		while (i < env->config.num_coders)
		{
			pthread_mutex_destroy(&env->dongles[i].mutex);
			pthread_cond_destroy(&env->dongles[i].cond);
			if (env->dongles[i].queue.requests)
				free(env->dongles[i].queue.requests);
			i++;
		}
		free(env->dongles);
	}
	if (env->coders)
		free(env->coders);
	pthread_mutex_destroy(&env->state_mutex);
	pthread_mutex_destroy(&env->log_mutex);
}

static int	init_global_mutexes(t_env *env)
{
	if (pthread_mutex_init(&env->state_mutex, NULL) != 0)
		return (0);
	if (pthread_mutex_init(&env->log_mutex, NULL) != 0)
		return (0);
	return (1);
}

static void	init_coders(t_env *env)
{
	int	i;

	i = 0;
	while (i < env->config.num_coders)
	{
		env->coders[i].id = i + 1;
		env->coders[i].compile_count = 0;
		env->coders[i].last_compile_start = 0;
		env->coders[i].left_dongle = i;
		env->coders[i].right_dongle = (i + 1) % env->config.num_coders;
		env->coders[i].env = env;
		i++;
	}
}

static int	init_dongles(t_env *env)
{
	int	i;

	i = 0;
	while (i < env->config.num_coders)
	{
		env->dongles[i].id = i + 1;
		env->dongles[i].is_taken = 0;
		env->dongles[i].holding_coder = 0;
		env->dongles[i].available_at = 0;
		env->dongles[i].queue.size = 0;
		env->dongles[i].queue.requests = malloc(sizeof(t_request)
				* env->config.num_coders);
		if (!env->dongles[i].queue.requests)
			return (0);
		if (pthread_mutex_init(&env->dongles[i].mutex, NULL) != 0)
			return (0);
		if (pthread_cond_init(&env->dongles[i].cond, NULL) != 0)
			return (0);
		i++;
	}
	return (1);
}

int	init_env(t_env *env)
{
	env->coders = NULL;
	env->dongles = NULL;
	env->start_time = 0;
	env->simulation_running = 1;
	if (!init_global_mutexes(env))
		return (0);
	env->coders = malloc(sizeof(t_coder) * env->config.num_coders);
	if (!env->coders)
		return (0);
	env->dongles = malloc(sizeof(t_dongle) * env->config.num_coders);
	if (!env->dongles)
	{
		free_env(env);
		return (0);
	}
	if (!init_dongles(env))
	{
		free_env(env);
		return (0);
	}
	init_coders(env);
	return (1);
}
