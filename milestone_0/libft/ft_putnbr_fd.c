/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 15:44:14 by amillan-          #+#    #+#             */
/*   Updated: 2025/11/20 15:59:45 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	long int	l_n;

	l_n = n;
	if (l_n < 0)
	{
		write(fd, "-", 1);
		l_n = -l_n;
	}
	if (l_n >= 10)
	{
		ft_putnbr_fd((l_n / 10), fd);
	}
	ft_putchar_fd((l_n % 10 + '0'), fd);
}
