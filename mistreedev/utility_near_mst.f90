

subroutine dist_from_line(x0, y0, z0, x1, y1, z1, xr, yr, zr, number_of_points, dist_para, dist_perp)
  ! will give the perpendicular and parallel distance from a line, not the distance from
  ! the line is given in units of the lines length.
  !
  ! Parameters
  ! ----------
  ! x0, y0, z0 : float
  !     The coordinate of one end of the line.
  ! x1, y1, z1 : float
  !     The coordinate of the other end of the line.
  ! xr, yr, zr : array_like
  !     The points we wish to check the distance to the line.
  ! number_of_points : integer
  !     The number of points being checked.
  !
  ! Returns
  ! -------
  ! dist_para : array_like
  !     The distance of points parallel to the line given in units of the of the lines length
  ! dist_perp : array_like
  !     The distance of points perpendicular to the line.

  implicit none

  integer, intent(in) :: number_of_points
  real, intent(in) :: x0, y0, z0, x1, y1, z1
  real, intent(in) :: xr(number_of_points), yr(number_of_points), zr(number_of_points)
  real, intent(out) :: dist_para(number_of_points), dist_perp(number_of_points)

  integer :: i
  real :: a, b, c, xnew, ynew, znew, dist_para_, dist_perp_

  a = x1 - x0
  b = y1 - y0
  c = z1 - z0

  do i=1, number_of_point
    dist_para_ = a*(xr(i) - x0) + b*(yr(i) - y0) + c*(zr(i) - z0)
    dist_para_ /= a**2. + b**2. + c**2.
    xnew = a*t + x0
    ynew = b*t + y0
    znew = c*t + z0
    dist_perp_ = sqrt((xr(i)-xnew)**2. + (yr(i)-ynew)**2. + (zr(i)-znew)**2.)
    dist_para(i) = dist_para_
    dist_perp(i) = dist_perp_
  end do

end subroutine dist_from_line
