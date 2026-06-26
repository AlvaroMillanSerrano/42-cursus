/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simulation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 12:18:59 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/15 12:19:01 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

int	try_acquire_both(t_coder *coder, t_dongle *left, t_dongle *right)
{
	long long	now;

	if (coder->env->config.num_coders == 1)
		return (0);
	lock_dongles_ordered(left, right);
	now = get_time_ms();
	if (!left->is_taken && !right->is_taken
		&& (left->queue.size == 0 || left->queue.requests[0].coder_id == coder->id)
		&& (right->queue.size == 0 || right->queue.requests[0].coder_id == coder->id)
		&& now >= left->available_at && now >= right->available_at)
	{
		left->is_taken = 1;
		left->holding_coder = coder->id;
		right->is_taken = 1;
		right->holding_coder = coder->id;
		print_status(coder, "has taken a dongle");
		print_status(coder, "has taken a dongle");
		pthread_mutex_unlock(&right->mutex);
		pthread_mutex_unlock(&left->mutex);
		return (1);
	}
	pthread_mutex_unlock(&right->mutex);
	pthread_mutex_unlock(&left->mutex);
	return (0);
}

void	push_to_required_heaps(t_coder *coder, t_request req)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &coder->env->dongles[coder->left_dongle];
	right = &coder->env->dongles[coder->right_dongle];
	pthread_mutex_lock(&left->mutex);
	heap_push(&left->queue, req, coder->env->config.scheduler_mode);
	pthread_mutex_unlock(&left->mutex);
	if (coder->env->config.num_coders > 1)
	{
		pthread_mutex_lock(&right->mutex);
		heap_push(&right->queue, req, coder->env->config.scheduler_mode);
		pthread_mutex_unlock(&right->mutex);
	}
}

void	release_required_heaps(t_coder *coder)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &coder->env->dongles[coder->left_dongle];
	right = &coder->env->dongles[coder->right_dongle];
	pthread_mutex_lock(&left->mutex);
	left->is_taken = 0;
	left->available_at = get_time_ms() + coder->env->config.cooldown;
	heap_pop(&left->queue, coder->env->config.scheduler_mode);
	pthread_cond_broadcast(&left->cond);
	pthread_mutex_unlock(&left->mutex);
	if (coder->env->config.num_coders > 1)
	{
		pthread_mutex_lock(&right->mutex);
		right->is_taken = 0;
		right->available_at = get_time_ms() + coder->env->config.cooldown;
		heap_pop(&right->queue, coder->env->config.scheduler_mode);
		pthread_cond_broadcast(&right->cond);
		pthread_mutex_unlock(&right->mutex);
	}
}

void	execute_compile_cycle(t_coder *coder)
{
	t_request	req;

	req.coder_id = coder->id;
	req.request_time = get_time_ms();
	pthread_mutex_lock(&coder->env->state_mutex);
	req.deadline = coder->last_compile_start + coder->env->config.time_burnout;
	pthread_mutex_unlock(&coder->env->state_mutex);
	push_to_required_heaps(coder, req);
	while (!is_sim_over(coder))
	{
		if (try_acquire_both(coder, &coder->env->dongles[coder->left_dongle],
				&coder->env->dongles[coder->right_dongle]))
			break ;
		usleep(100);
	}
	if (is_sim_over(coder))
		return ;
	pthread_mutex_lock(&coder->env->state_mutex);
	coder->last_compile_start = get_time_ms();
	coder->compile_count++;
	pthread_mutex_unlock(&coder->env->state_mutex);
	print_status(coder, "is compiling");
	smart_sleep(coder->env->config.time_compile, coder->env);
	release_required_heaps(coder);
	check_and_stop_simulation(coder);
}

void	*coder_routine(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	while (1)
	{
		if (is_sim_over(coder))
			break ;
		execute_compile_cycle(coder);
		if (is_sim_over(coder)
			|| coder->compile_count >= coder->env->config.num_compiles)
			break ;
		print_status(coder, "is debugging");
		smart_sleep(coder->env->config.time_debug, coder->env);
		if (is_sim_over(coder))
			break ;
		print_status(coder, "is refactoring");
		smart_sleep(coder->env->config.time_refactor, coder->env);
	}
	return (NULL);
}
