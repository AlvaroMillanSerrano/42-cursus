/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/10 09:33:26 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/10 09:33:47 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

static int	start_threads(t_env *env, pthread_t *monitor)
{
	int	i;

	env->start_time = get_time_ms();
	i = 0;
	while (i < env->config.num_coders)
	{
		env->coders[i].last_compile_start = env->start_time;
		if (pthread_create(&env->coders[i].thread, NULL,
				coder_routine, &env->coders[i]) != 0)
			return (0);
		i++;
	}
	if (pthread_create(monitor, NULL, monitor_routine, env) != 0)
		return (0);
	return (1);
}

static void	join_threads(t_env *env, pthread_t monitor)
{
	int	i;

	i = 0;
	while (i < env->config.num_coders)
	{
		pthread_join(env->coders[i].thread, NULL);
		i++;
	}
	pthread_join(monitor, NULL);
}

int	main(int argc, char **argv)
{
	t_env		env;
	pthread_t	monitor;

	if (!parse_args(&env.config, argc, argv))
		return (1);
	if (!init_env(&env))
		return (1);
	if (!start_threads(&env, &monitor))
	{
		pthread_mutex_lock(&env.state_mutex);
		env.simulation_running = 0;
		pthread_mutex_unlock(&env.state_mutex);
		join_threads(&env, monitor);
		free_env(&env);
		return (1);
	}
	join_threads(&env, monitor);
	free_env(&env);
	return (0);
}
