/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/10 09:33:58 by amillan-          #+#    #+#             */
/*   Updated: 2026/06/10 09:34:08 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "codexion.h"

int	val_positive_number(char *str)
{
	int	i;

	i = 0;
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	if (atoi(str) <= 0)
		return (0);
	return (1);
}

char	*get_arg(int i)
{
	char	*arg_names[8];

	arg_names[0] = "program_name";
	arg_names[1] = "number_of_coders";
	arg_names[2] = "time_to_burnout";
	arg_names[3] = "time_to_compile";
	arg_names[4] = "time_to_debug";
	arg_names[5] = "time_to_refactor";
	arg_names[6] = "number_of_compiles_required";
	arg_names[7] = "dongle_cooldown";
	return (arg_names[i]);
}

int	get_mode(char *str)
{
	if (strcmp(str, "fifo") == 0)
		return (1);
	if (strcmp(str, "edf") == 0)
		return (2);
	printf("Error. Invalid scheduler\n");
	return (0);
}

int	val_args(char **args)
{
	int	i;

	i = 1;
	while (i <= 7)
	{
		if (!val_positive_number(args[i]))
		{
			printf("Error: invalid value for %s\n", get_arg(i));
			return (0);
		}
		i++;
	}
	return (1);
}

int	parse_args(t_config *config, int argc, char **argv)
{
	if (argc != 9)
	{
		printf("Error. Missing arguments\n");
		return (0);
	}
	if (!val_args(argv))
		return (0);
	config->num_coders = atoi(argv[1]);
	config->time_burnout = atoi(argv[2]);
	config->time_compile = atoi(argv[3]);
	config->time_debug = atoi(argv[4]);
	config->time_refactor = atoi(argv[5]);
	config->num_compiles = atoi(argv[6]);
	config->cooldown = atoi(argv[7]);
	config->scheduler_mode = get_mode(argv[8]);
	if (config->scheduler_mode == 0)
		return (0);
	return (1);
}
