/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simulation_utils.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/16 10:35:05 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/16 10:35:18 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

void	lock_dongles_ordered(t_dongle *left, t_dongle *right)
{
	if (left->id < right->id)
	{
		pthread_mutex_lock(&left->mutex);
		pthread_mutex_lock(&right->mutex);
	}
	else
	{
		pthread_mutex_lock(&right->mutex);
		pthread_mutex_lock(&left->mutex);
	}
}

int	can_acquire(t_coder *coder, t_dongle *left, t_dongle *right,
		long long now)
{
	if (left->is_taken || right->is_taken)
		return (0);
	if (left->queue.size != 0
		&& left->queue.requests[0].coder_id != coder->id)
		return (0);
	if (right->queue.size != 0
		&& right->queue.requests[0].coder_id != coder->id)
		return (0);
	if (now < left->available_at || now < right->available_at)
		return (0);
	return (1);
}

int	is_sim_over(t_coder *coder)
{
	int	over;

	pthread_mutex_lock(&coder->env->state_mutex);
	over = !coder->env->simulation_running;
	pthread_mutex_unlock(&coder->env->state_mutex);
	return (over);
}

void	check_and_stop_simulation(t_coder *coder)
{
	int	i;
	int	all_done;

	pthread_mutex_lock(&coder->env->state_mutex);
	if (coder->compile_count >= coder->env->config.num_compiles)
	{
		i = 0;
		all_done = 1;
		while (i < coder->env->config.num_coders)
		{
			if (coder->env->coders[i].compile_count
				< coder->env->config.num_compiles)
				all_done = 0;
			i++;
		}
		if (all_done)
			coder->env->simulation_running = 0;
	}
	pthread_mutex_unlock(&coder->env->state_mutex);
}
