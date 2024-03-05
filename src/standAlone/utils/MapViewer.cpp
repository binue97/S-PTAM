/**
 * Authors: Binue
 */

#include "MapViewer.hpp"

MapViewer::MapViewer(int32_t mapWidth, int32_t mapHeight) : offset_(mapWidth/2, mapHeight/2), mapSize_(mapWidth, mapHeight), canvas_(mapSize_, CV_8UC3, cv::Scalar(0, 0, 0))
{
  cv::namedWindow("MapView");
  cv::setMouseCallback("MapView", mouseCallback, this);
}

void MapViewer::setMap(sptam::Map& map)
{
  mapPtr_ = &map;
}

void MapViewer::drawMap()
{
  clear();
  if (mapPtr_ != nullptr)
  {
    drawTrajectory();
    drawLandmarks();
  }
  cv::imshow("MapView", canvas_);
  cv::waitKey(1);
}

void MapViewer::clear()
{
  canvas_ = cv::Scalar(0, 0, 0);
}

void MapViewer::drawTrajectory()
{
  const auto& keyframes = mapPtr_->getKeyframes();

  for (const auto& keyframe : keyframes)
  {
    const CameraPose& pose = keyframe->GetCameraPose();
    const Eigen::Vector3d& position = pose.GetPosition();

    // Visualize pose with Axes.
    constexpr double axisLength = 1.0;
    Eigen::Vector3d x_axis = pose.ToWorld(Eigen::Vector3d(axisLength, 0, 0));
    Eigen::Vector3d z_axis = pose.ToWorld(Eigen::Vector3d(0, 0, axisLength));

    cv::line(canvas_, world_to_image(position), world_to_image(x_axis), cv::Scalar(0, 0, 255), 2);
    cv::line(canvas_, world_to_image(position), world_to_image(z_axis), cv::Scalar(0, 255, 0), 2);
  }
}

void MapViewer::drawLandmarks()
{
  const auto& mapPoints = mapPtr_->getMapPoints();

  for (const auto& mapPoint : mapPoints)
  {
    const Eigen::Vector3d& position = mapPoint->GetPosition();

    cv::circle(canvas_, world_to_image(position), 1, cv::Scalar(150, 150, 150), -1);
  }
}

cv::Point2i MapViewer::world_to_image(const Eigen::Vector3d& world_point) const
{
  cv::Point2i image_point (world_point.x() * scale_, -world_point.z() * scale_);
  image_point += offset_;

  return image_point;
}

void MapViewer::mouseCallback(int32_t event, int32_t x, int32_t y, int32_t flags, void* data)
{
  auto viewerPtr = static_cast<MapViewer*>(data);
  static int32_t prev_x = 0;
  static int32_t prev_y = 0;

  if (event == cv::EVENT_MOUSEWHEEL)
  {
    double delta_scale = (cv::getMouseWheelDelta(flags) > 0) ? 1.1 : 0.9;
    viewerPtr->scale_ *= delta_scale;

    const int32_t cx = viewerPtr->offset_.x;
    const int32_t cy = viewerPtr->offset_.y;

    viewerPtr->offset_.x = static_cast<int32_t>(delta_scale * cx + (1 - delta_scale) * prev_x);
    viewerPtr->offset_.y = static_cast<int32_t>(delta_scale * cy + (1 - delta_scale) * prev_y);
  }
  else if (event == cv::EVENT_LBUTTONDOWN)
  {
    prev_x = x;
    prev_y = y;
  }
  else if (event == cv::EVENT_MOUSEMOVE)
  {
    if (flags & cv::EVENT_FLAG_LBUTTON)
    {
      int32_t delta_x = x - prev_x;
      int32_t delta_y = y - prev_y;
      viewerPtr->offset_ += cv::Point2i(delta_x, delta_y);
    }
    prev_x = x;
    prev_y = y;
  }
}

