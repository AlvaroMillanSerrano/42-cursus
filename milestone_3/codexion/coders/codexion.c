/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 09:21:22 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/15 09:21:27 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

long long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return ((tv.tv_sec * 1000LL) + (tv.tv_usec / 1000));
}

void	print_status(t_coder *coder, const char *status)
{
	long long	now;

	pthread_mutex_lock(&coder->env->state_mutex);
	if (!coder->env->simulation_running && strcmp(status, "burned out") != 0)
	{
		pthread_mutex_unlock(&coder->env->state_mutex);
		return ;
	}
	now = get_time_ms() - coder->env->start_time;
	pthread_mutex_lock(&coder->env->log_mutex);
	printf("%lld %d %s\n", now, coder->id, status);
	pthread_mutex_unlock(&coder->env->log_mutex);
	pthread_mutex_unlock(&coder->env->state_mutex);
}

void	smart_sleep(long long ms, t_env *env)
{
	long long	start;

	start = get_time_ms();
	while (1)
	{
		pthread_mutex_lock(&env->state_mutex);
		if (!env->simulation_running)
		{
			pthread_mutex_unlock(&env->state_mutex);
			break ;
		}
		pthread_mutex_unlock(&env->state_mutex);
		if (get_time_ms() - start >= ms)
			break ;
		usleep(50);
	}
}

void	take_single_dongle(t_coder *coder, t_dongle *dongle)
{
	t_request	req;

	pthread_mutex_lock(&dongle->mutex);
	req.coder_id = coder->id;
	req.request_time = get_time_ms();
	req.deadline = coder->last_compile_start + coder->env->config.time_burnout;
	heap_push(&dongle->queue, req, coder->env->config.scheduler_mode);
	while (1)
	{
		if (!dongle->is_taken && dongle->queue.requests[0].coder_id == coder->id
			&& get_time_ms() >= dongle->available_at)
		{
			dongle->is_taken = 1;
			dongle->holding_coder = coder->id;
			heap_pop(&dongle->queue, coder->env->config.scheduler_mode);
			print_status(coder, "has taken a dongle");
			break ;
		}
		pthread_cond_wait(&dongle->cond, &dongle->mutex);
	}
	pthread_mutex_unlock(&dongle->mutex);
}

void	release_single_dongle(t_coder *coder, t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->mutex);
	dongle->is_taken = 0;
	dongle->holding_coder = 0;
	dongle->available_at = get_time_ms() + coder->env->config.cooldown;
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
}
